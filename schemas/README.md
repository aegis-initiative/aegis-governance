# AEGIS Schema Pack

This directory contains machine-validated schema definitions for AEGIS protocol and governance artifacts.

## Structure

- `common/` reusable schema primitives
- `agp/` AGP protocol message schemas
- `capability/` capability registry schemas
- `governance/` governance envelope and event schemas
- `examples/` sample payloads validated in CI

## Validation

CI validates schemas with `ajv-cli` and checks that examples conform to their corresponding schemas.
