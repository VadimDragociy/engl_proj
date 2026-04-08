# Phystech.(p)Ass

An MVP face recognition access system developed for the project fair of the Foreign Languages Department at MIPT, Russia.

## Project summary

The main goal of this project is to reduce queues in campus buildings by introducing Face ID-based access control, while also making entry easier for students who often forget their ID cards.

At the current stage, we have built a working MVP with the following core features:

- Face ID pipeline based on InsightFace (`buffalo_l`)
- A lightweight SQLite3 database for storing embeddings
- A simple web interface for demonstration and onboarding new users

The project is still in active development. Planned improvements include scalable vector search with HNSW, integration with local turnstiles over the local network, proximity-based activation to avoid running the system 24/7, and additional business logic and security measures.

## Technologies

1. **Face embeddings:** `insightface` (`buffalo_l`)
2. **Database:** `sqlite3`
3. **UI:** FastAPI + HTML

## How it works

- Face embeddings are extracted directly from the live video feed.
- The system currently runs at around **20 FPS** on an **RTX 3050 Laptop GPU (4 GB VRAM)**.
- Each new embedding is compared against entries stored in the database.
- The web page is used both for adding new users to the database and for face recognition.

## Media

The `resources` folder contains project media materials:

- `resources/hnsw.png` — illustration of the HNSW approach
- `resources/demo.mp4` — video demonstration of the project

## Project Future

### HNSW
![hnsw](resources\hnsw.png)

HNSW (Hierarchical Navigable Small World) is an approximate nearest-neighbor search method for vectors.

It works by building several graph layers:

- The top layers are sparse and act like a coarse map.
- The bottom layer is dense and contains most vectors.

To search, it starts at the top with a random entry point, then repeatedly moves to closer neighbors while descending layer by layer. At each layer it does a greedy walk: from the current node, it checks nearby nodes and moves to the one that looks closest to the query.

Why it is fast:

- The upper layers let it jump quickly to the right region.
- The lower layer does fine-grained search only around promising candidates.
- It avoids scanning all vectors, so search is much faster than brute force.

Why it works well:

- The graph is built so each node connects to a small set of useful neighbors.
- That creates “small-world” shortcuts, which makes navigation efficient.

### Proximity sensor + top 1 candidate
![proximity](resources\proximity.png)

1) Image inference will only work when someone is up close -> thus saved time
2) We will only inference 1 closest face -> no trespassing and no detection of every face in the frame

## Getting started

These are requirements for CPU version
GPU version will require you to install onnxruntime-gpu, proper Cudnn and Cuda
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```