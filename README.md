# Action: generate docker build matrix
> This repository is only a mirror. Development and testing is done on a private gitea server.

This action generates a docker build matrix from a json-formatted list of versions

## Parameters

The following parameters can be used as `step.with` keys:

| Name               | Type   | Default | Required |Description                       |
| ------------------ | ------ | ------- |--------- |--------------------------------- |
| `versions      `   | String |         | yes      | Json Formatted List as a String  |


## Example usage

```yaml
jobs:
  publish:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Generate docker build matrix
      uses: ednz-cloud/docker-matrix-generator@v1
      with:
        versions: '["2.2.8","2.2.7","2.2.4","2.2.3","2.1.5","2.1.4","2.1.3","2.1.2","2.1.1","2.1.0","2.0.20","2.0.19","2.0.18","2.0.17","2.0.16","2.0.15","2.0.14","2.0.13"]'
```