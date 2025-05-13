#!/usr/bin/env python3
import logging
import random
import shutil
import sys
from typing import List, Tuple

import numpy as np
from durations import Duration

from timeeval import TimeEval, Datasets, TrainingType
from timeeval.constants import HPI_CLUSTER
from timeeval.remote import RemoteConfiguration
from timeeval.resource_constraints import ResourceConstraints, GB
from timeeval.utils.metrics import Metric
from timeeval_experiments.algorithm_configurator import AlgorithmConfigurator
from timeeval_experiments.algorithms import *


# Setup logging
logging.basicConfig(
    filename="timeeval.log",
    filemode="a",
    level=logging.INFO,
    # force=True,
    format="%(asctime)s %(levelname)6.6s - %(name)20.20s: %(message)s",
)

random.seed(42)
np.random.rand(42)
MAX_CONTAMINATION = 0.1
MIN_ANOMALIES = 1


def gutentag():
    dm = Datasets(HPI_CLUSTER.akita_test_case_path, create_if_missing=False)
    # Select all test case datasets
    datasets = dm.select()
    return dm, datasets


def benchmark():
    dm = Datasets(HPI_CLUSTER.akita_benchmark_path, create_if_missing=False)

    # Select datasets
    datasets: List[Tuple[str, str]] = []
    datasets += dm.select(collection_name="CalIt2", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="Daphnet", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # no datasets match criteria for Dodgers
    # datasets += dm.select(collection_name="Dodgers", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # select 4 datasets of large-timeseries collection Exathlon
    datasets += random.sample(dm.select(collection_name="Exathlon", train_type=TrainingType.SUPERVISED.value), 2)
    datasets += random.sample(dm.select(collection_name="Exathlon", train_type=TrainingType.SEMI_SUPERVISED.value), 2)
    datasets += dm.select(collection_name="GHL", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="Genesis", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # GutenTAG uses a separate run
    # select 4 datasets of large-timeseries collection IOPS
    datasets += random.sample(dm.select(collection_name="IOPS", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES), 4)
    # include everything from KDD-TSAD!
    datasets += dm.select(collection_name="KDD-TSAD")
    datasets += dm.select(collection_name="Keogh", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # exclude Kitsune completely, bc it's too large!
    # datasets += random.sample(dm.select(collection_name="Kitsune", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES), 4)
    # exclude LTDB completely, bc it's too large!
    # datasets += random.sample(dm.select(collection_name="LTDB", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES), 4)
    datasets += dm.select(collection_name="MGAB", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="MITDB", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="Metro", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # include everything from NAB!
    datasets += dm.select(collection_name="NAB")
    datasets += dm.select(collection_name="NASA-MSL", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="NASA-SMAP", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="OPPORTUNITY", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # no datasets match criteria for Occupancy
    datasets += dm.select(collection_name="Occupancy", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="SMD", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    # no datasets match criteria for SSA, bc contamination > 0.14 for all datasets
    # datasets += dm.select(collection_name="SSA")
    datasets += dm.select(collection_name="SVDB", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    datasets += dm.select(collection_name="WebscopeS5", max_contamination=MAX_CONTAMINATION, min_anomalies=MIN_ANOMALIES)
    return dm, datasets


def run(dm, datasets, is_gutentag: bool = False):
    configurator = AlgorithmConfigurator(config_path="param-config.json")

    algorithms = [
        deepant()
    ]
    print(f"Selecting {len(algorithms)} algorithms")

    print("Configuring algorithms...")
    configurator.configure(algorithms, perform_search=False)

    print("\nDatasets:")
    print("=====================================================================================")
    for collection in np.unique([c for (c, d) in datasets]):
        print(collection)
        cds = sorted([d for (c, d) in datasets if c == collection])
        for cd in cds:
            print(f"  {cd}")
    print("=====================================================================================\n\n")

    print("\nParameter configurations:")
    print("=====================================================================================")
    for algo in algorithms:
        print(algo.name)
        for param in algo.param_config:
            print(f"  {param}")
    print("=====================================================================================\n\n")
    sys.stdout.flush()

    cluster_config = RemoteConfiguration(
        scheduler_host=HPI_CLUSTER.odin01,
        worker_hosts=HPI_CLUSTER.nodes
    )
    limits = ResourceConstraints(
        tasks_per_host=10,
        task_cpu_limit=1.,
        task_memory_limit=3 * GB,
        use_preliminary_model_on_train_timeout=True,
        train_timeout=Duration("2 hours"),
        execute_timeout=Duration("2 hours"),
    )
    timeeval = TimeEval(dm, datasets, algorithms,
                        repetitions=1,
                        distributed=True,
                        remote_config=cluster_config,
                        resource_constraints=limits,
                        skip_invalid_combinations=True,
                        force_dimensionality_match=False,
                        force_training_type_match=is_gutentag,
                        metrics=[Metric.ROC_AUC, Metric.PR_AUC, Metric.RANGE_PR_AUC, Metric.AVERAGE_PRECISION],
                        )

    # copy parameter configuration file to results folder
    timeeval.results_path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(configurator.config_path, timeeval.results_path)

    timeeval.run()
    print(timeeval.get_results(aggregated=True, short=True))


def main():
    print("\n\n##################################")
    print("# Running on GutenTAG collection #")
    print("##################################")
    dm, datasets = gutentag()
    run(dm, datasets, is_gutentag=True)

    print("\n\n###################################")
    print("# Running on benchmark collection #")
    print("###################################")
    dm, datasets = benchmark()
    run(dm, datasets, is_gutentag=False)


if __name__ == "__main__":
    main()
