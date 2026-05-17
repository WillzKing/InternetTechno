Docker Image Optimization Report

Project code: likes-s15

## Image Size

### Standard image (single-stage, python:3.11-slim)
- Size: ~350 MB
- Includes build tools and pip cache

### Optimized image (multi-stage)
- Size: ~200 MB
- Builder stage installs dependencies
- Final stage copies only ready packages

## Image Layers

1. FROM python:3.11-slim AS builder - base image (~150 MB)
2. COPY requirements.txt - copy dependencies file
3. RUN pip install - install packages (~50 MB)
4. FROM python:3.11-slim - new base image
5. COPY --from=builder - copy only installed packages
6. COPY . - copy application code
7. CMD - run command

## Build and Run Commands

Build:
  docker build -t week10-app .

Run:
  docker run -d -p 8174:8174 --name week10-container week10-app

## Conclusions

Multi-stage build reduced final image size by ~40% by:
- Excluding build tools (gcc, make, etc.)
- Excluding pip cache
- Proper layer ordering (requirements.txt copied before code)

.dockerignore excludes unnecessary files from build context.
