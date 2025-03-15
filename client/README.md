# Client (Angular)

This folder contains the front-end application generated with [Angular CLI](https://github.com/angular/angular-cli).

---

## Table of Contents

- [Development Server](#development-server)
- [Code Scaffolding](#code-scaffolding)
- [Building](#building)
- [Running Unit Tests](#running-unit-tests)
- [Running End-to-End Tests](#running-end-to-end-tests)
- [Additional Resources](#additional-resources)

---

## Development Server

In this directory, make sure you have the required dependencies installed:

```bash
npm install
```

Then, start a local development server:

```bash
ng serve
```

Open your browser at [http://localhost:4200/](http://localhost:4200/) to view the application.  
Any changes to source files will automatically reload the application.

---

## Code Scaffolding

Use Angular CLI’s scaffolding commands to generate new parts of your application:

```bash
ng generate component component-name
```

For other schematics such as directives or pipes, run:

```bash
ng generate --help
```

---

## Building

Compile the project:

```bash
ng build
```

The build artifacts will be placed in the `dist/` folder.  
By default, this is a production-optimized build. You can pass different configuration flags if needed (e.g.,
`--configuration development`).

---

## Running Unit Tests

Execute unit tests via the [Karma](https://karma-runner.github.io) test runner:

```bash
ng test
```

---

## Running End-to-End Tests

Angular CLI no longer includes an e2e suite by default. You can add one of your choice (e.g., Cypress, Protractor).  
Once configured, typically you would run:

```bash
ng e2e
```

---

## Additional Resources

- For more information on Angular CLI commands, see the [Angular CLI Reference](https://angular.dev/tools/cli).
- If you need to serve the app in a production-like environment, look into server-side rendering (SSR) using frameworks
  such as Express, or see Angular SSR documentation.
- For details on the backend and environment configuration, check the main **heatmap-iot-analytics** README and the
  **/web** README in this project.