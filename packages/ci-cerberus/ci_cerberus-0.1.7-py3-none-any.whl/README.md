# 🐕 ci-cerberus

Guarding the gates of your GitHub workflows

## What is it?

ci-cerberus is a tool designed to locate third-party GitHub Actions in your workflows, and report any known vulnerabilities back to you.

## Running ci-cerberus

The easiest way to run this tool is with [pipx](https://pipx.pypa.io/stable/).

You can install it (if you don't already have it) by following [the instructions here](https://github.com/pypa/pipx)

### Scan

`scan` is currently the only command available in ci-cerberus.

It looks for workflows in your `.github/workflows` folder, and finds any third-party actions. It then checks the [NIST NVD](https://nvd.nist.gov/) for any known vulnerabilities and reports them back to you

Navigate to the root of the repository you want to scan and run

```sh
pipx run ci-cerberus scan
```

### Debug Mode

If you want to see more information about what this tool is doing under the hood, you can enable debug mode by supplying the `-d` or `--debug` flag **before** the command

```sh
pipx run ci-cerberus -d scan
```

### Help

If you're stuck, you can pull up the help text any time by running

```sh
pipx run ci-cerberus -h
```

## Notes

This tool was created as a project for one of my modules on the Masters program I'm currently enrolled in at Abertay University.

If you're reading this, then you're probably one of my lecturers 👋🏻
