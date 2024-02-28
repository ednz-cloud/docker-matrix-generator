# Action: generate docker build matrix
> This repository is only a mirror. Development and testing is done on a private gitea server.

This action generates a docker build matrix from a json-formatted list of versions

## Parameters

The following parameters can be used as `step.with` keys:

| Name               | Type   | Default | Required |Description                       |
| ------------------ | ------ | ------- |--------- |--------------------------------- |
| `versions      `   | String |         | yes      | comma separated list of versions |


## Example usage

```yaml
jobs:
  publish:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Generate docker build matrix
      uses: ednz-cloud/docker-matrix-generator@v1
      with:
        versions: 2.2.8, 2.2.7, 2.2.4, 2.2.3
```