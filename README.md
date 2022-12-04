# secret-santa

## About

A simple web application to help manage my family's yearly Secret Santa
tradition. `utils/*` provides the core functions for tracking and managing the
users.

In `utils/randomize_santas.py`, the algorithm for determining who get who is as follows:

1. Use a circular queue to act as a directed graph with each node in the queue
   being linked to the next
2. Traverse the queue and if the next node should not be connected to the
   current then append current node to the end of the queue and pop the next
   node in the queue
3. Continue in this manner until the queue is exhausted or until a node is seen
   again (i.e. cannot create a complete network with current settings)
   
## Screenshot

![Screenshot_20221203_155247](https://user-images.githubusercontent.com/12501720/205467577-0c78c20c-5dfa-4e1d-aa5e-d7f94d0519e3.png)

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
