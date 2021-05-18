# GitHub action to fetch secrets from PasswordState

With the 'Get passwordstate secret action, you can fetch secrets from [PasswordState](https://www.clickstudios.com.au/) and consume in your GitHub Action workflows.

Secrets fetched will be set as outputs of the Passwordstate action and can be consumed in subsequent action in the workflow.
In addition, secrets are also set as environment variables. All the variables are automatically maskesd if printed to the console or logs.

## Example

find below a sample workflow to use the passwordstate GitHub action.

``` yaml

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # checkout the repo
    - uses: actions/checkout@master
    - uses: Stijnc/get-passwordstate-secrets@v1
      with:
        url: "https://krypto.dexmach.com"
        secrets: 'azUsername1, azUsername2'
      id: myGetSecretAction
    - run: echo "This is my secret ${{ steps.myGetSecretAction.output.azUsername1 }}"

```

### retrieving your API key

to complete