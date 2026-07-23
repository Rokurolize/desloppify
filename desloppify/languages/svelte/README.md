# Svelte language integration

The Svelte plugin owns `.svelte` component files as an independent language state.

It runs project-local Svelte Check for component compilation, type, markup, and style diagnostics, then filters machine output to `.svelte` paths so JavaScript and TypeScript diagnostics remain in their own states. It also runs project-local ESLint with an explicit `.svelte` glob.

The TypeScript dependency graph may still read imports from Svelte components to preserve cross-language importer edges. That graph participation does not make Svelte components TypeScript scan inputs.
