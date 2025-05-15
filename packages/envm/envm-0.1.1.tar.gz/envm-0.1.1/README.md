
CLI to manage environments variables, the idea is because everyday I have to work with .env files with different projects and environments like dev, staging and local.

## Installation

To install the package, simply run:

```bash
pip install envm
```


## Examples:

1. Save the current .env (environment) file in the database environments
```bash
$ envm save users.dev
```

2. Use a file called .env in my current path:
```bash
$ envm use users.dev
```

3. (WIP) The next command should "export" the environments in my current shell session:
```bash
envm export users.dev
```

4. (WIP) Clean my current env space (--envm flag is optional)
```bash
envm clean --envm users.prod
```
