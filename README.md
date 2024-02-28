# Action: generate docker build matrix
> This repository is only a mirror. Development and testing is done on a private gitea server.

This action generates a docker build matrix from a comma-separated list of versions

## Parameters

The following parameters can be used as `step.with` keys:

| Name               | Type   | Default | Required |Description                       |
| ------------------ | ------ | ------- |--------- |--------------------------------- |
| `versions`         | String |         | yes      | comma separated list of versions |


## Use case

When building containers for multiple versions (for example, when building images for software developed somewhere else), you often need/want to be able to automatically tag images with `latest`, `major`, and `major.minor` versions automatically.

This action allows you to generate a json object that can be used to build these images, base on a list of versions.

For an input like:

`2.2.8,2.2.7,2.2.4,2.2.3`

It will output:

```json
[
  {
    "version": "2.2.8",
    "is_latest": true,
    "is_latest_major": true,
    "major_version": "2",
    "is_latest_minor": true,
    "minor_version": "2.2"
  },
  {
    "version": "2.2.7",
    "is_latest": false,
    "is_latest_major": false,
    "major_version": "2",
    "is_latest_minor": false,
    "minor_version": "2.2"
  },
  {
    "version": "2.2.4",
    "is_latest": false,
    "is_latest_major": false,
    "major_version": "2",
    "is_latest_minor": false,
    "minor_version": "2.2"
  },
  {
    "version": "2.2.3",
    "is_latest": false,
    "is_latest_major": false,
    "major_version": "2",
    "is_latest_minor": false,
    "minor_version": "2.2"
  }
]
```

This matrix can then be built to automatically tag your images with the correct tags, using the [docker/metadata-action](https://github.com/docker/metadata-action) action.

```yaml
- name: Prepare container metadata
  id: metadata
  uses: docker/metadata-action@v5
  with:
    images: ${{ env.IMAGE_NAME }}
    flavor: |
      latest=auto
    labels: |
      org.opencontainers.image.authors=${{ github.repository_owner }}
      org.opencontainers.image.created=${{ needs.prepare.outputs.date }}
      org.opencontainers.image.url=${{ github.event.repository.html_url }}
      org.opencontainers.image.documentation=${{ github.event.repository.html_url }}
      org.opencontainers.image.source=${{ github.event.repository.html_url }}
      org.opencontainers.image.version=${{ matrix.versions.version }}
    tags: |
      type=raw,value=${{ matrix.versions.version }},enable=true
      type=raw,value=${{ matrix.versions.minor_version }},enable=${{ matrix.versions.is_latest_minor }}
      type=raw,value=${{ matrix.versions.major_version }},enable=${{ matrix.versions.is_latest_major }}
      type=raw,value=latest,enable=${{ matrix.versions.is_latest }}
```

## Example usage

```yaml
jobs:
  define:
    outputs:
      version_matrix: ${{ steps.docker-build-matrix.outputs.version_matrix }}
    - name: Checkout Code
      uses: actions/checkout@v4

    - id: docker-build-matrix
      name: Generate docker build matrix
      uses: ednz-cloud/docker-matrix-generator@v1
      with:
        versions: 2.2.8, 2.2.7, 2.2.4, 2.2.3

  publish:
    runs-on: ubuntu-latest
    needs: define
    strategy:
      matrix:
        versions: ${{ fromJson(needs.define.outputs.version_matrix) }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup buildx
        uses: docker/setup-buildx-action@v3

      - name: Setup QEMU
        uses: docker/setup-qemu-action@v3

      - name: Login to container registry
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_API_USERNAME }}
          password: ${{ secrets.DOCKERHUB_API_TOKEN }}

      - name: Prepare container metadata
        id: metadata
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          flavor: |
            latest=auto
          labels: |
            org.opencontainers.image.authors=${{ github.repository_owner }}
            org.opencontainers.image.created=${{ needs.prepare.outputs.date }}
            org.opencontainers.image.url=${{ github.event.repository.html_url }}
            org.opencontainers.image.documentation=${{ github.event.repository.html_url }}
            org.opencontainers.image.source=${{ github.event.repository.html_url }}
            org.opencontainers.image.version=${{ matrix.versions.version }}
          tags: |
            type=raw,value=${{ matrix.versions.version }},enable=true
            type=raw,value=${{ matrix.versions.minor_version }},enable=${{ matrix.versions.is_latest_minor }}
            type=raw,value=${{ matrix.versions.major_version }},enable=${{ matrix.versions.is_latest_major }}
            type=raw,value=latest,enable=${{ matrix.versions.is_latest }}

      - name: Build and publish
        id: build-and-push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ (github.event_name != 'pull_request') || (env.FORCE_PUBLISH == 'true') }}
          tags: ${{ steps.metadata.outputs.tags }}
          labels: ${{ steps.metadata.outputs.labels }}
          platforms: ${{ env.BUILD_PLATFORMS }}
          build-args: KEEPALIVED_VERSION=${{ matrix.versions.version }}
```