# BIOM9450 Project

## Getting Started

1. As a bare minimum, this project requires Node, Python and PostgreSQL to be installed.
2. See [Database Documentation](./db/README.md) for setting up the database.
3. See [Backend Documentation](./backend/README.md) for setting up the backend server.
4. See [Frontend Documentation](./cancer_insight_web/README.md) for setting up the frontend server.

## Architecture

The choice of a client-server architecture with Vue.js as the frontend and Python Flask-RESTx as
the backend reflects a focus on modularity, scalability, and ease of development. Vue.js provides
a reactive and efficient framework for building dynamic, user-friendly interfaces, allowing seamless
interaction with the backend. Flask-RESTx complements this by offering a lightweight and flexible
backend framework that simplifies the creation of RESTful APIs, ideal for handling structured
communication between the frontend and server. This separation of concerns enables independent
development, testing, and scaling of the frontend and backend, while the RESTful design ensures
compatibility with other potential clients or services in the future. Furthermore, using a separate
server for the backend enables more powerful hardware for the MOGONET algorithm, which on a CPU alone
may take more than 12 mins to run.
