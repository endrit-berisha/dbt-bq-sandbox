import argparse
import json
import os
import subprocess
from google.cloud import bigquery
from google.oauth2 import service_account

def create_dataset(client, dataset_id):
  dataset = bigquery.Dataset(dataset_id)
  dataset.location = "US"
  dataset = client.create_dataset(dataset, exists_ok=True)
  print(f"Created dataset {dataset.dataset_id}")

def delete_dataset(client, dataset_id):
  client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
  print(f"Deleted dataset {dataset_id}")

def run_dbt_command(command):
  result = subprocess.run(command, shell=True, capture_output=True, text=True)
  if result.returncode != 0:
    print(f"Command failed: {command}")
    print(f"Result: {result}")
    raise Exception(f"DBT command failed: {command}")
  print(result.stdout)

def main(project_id, dataset_id, credentials_json, dbt_path, dbt_target, cleanup=False):
  credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
  client = bigquery.Client(credentials=credentials, project=project_id)

  full_dataset_id = f"{project_id}.{dataset_id}"

  if cleanup: # Drop PR dataset
    delete_dataset(client, full_dataset_id)
    return

  if "pr_" in dataset_id:
    create_dataset(client, full_dataset_id)

  try:
    run_dbt_command(f"cd {dbt_path} && dbt deps")
    run_dbt_command(f"cd {dbt_path} && dbt debug --profiles-dir . --target {dbt_target}")
    run_dbt_command(f"cd {dbt_path} && dbt test --profiles-dir . --target {dbt_target}")
    run_dbt_command(f"cd {dbt_path} && dbt run --profiles-dir . --target {dbt_target}")
  except Exception as e:
    print(e)
    if "pr_" in dataset_id:
      print("Cleaning up PR dataset due to failure.")
      delete_dataset(client, full_dataset_id)
    raise

  if "pr_" in dataset_id:
    delete_dataset(client, full_dataset_id)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Manage PR-specific BigQuery dataset")
  parser.add_argument("--project_id", required=True, help="GCP Project ID")
  parser.add_argument("--dataset_id", required=True, help="BigQuery Dataset ID")
  parser.add_argument("--credentials_json", required=True, help="GCP Service Account JSON")
  parser.add_argument("--dbt_path", required=True, help="Path to DBT project")
  parser.add_argument("--dbt_target", required=True, help="DBT target")
  parser.add_argument("--cleanup", action='store_true', help="Cleanup the dataset")

  args = parser.parse_args()
  main(args.project_id, args.dataset_id, args.credentials_json, args.dbt_path, args.dbt_target, args.cleanup)
