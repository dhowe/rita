import type { Options } from 'tsup';
import { defineConfig } from 'tsup';
import { esbuildPluginVersionInjector } from 'esbuild-plugin-version-injector';

const opts: Options = {
  name: "rita",
  entry: { rita: 'src/rita.js' },
  outDir: 'dist',
  watch: false,
  clean: true,
  minify: true,
  sourcemap: true,
  dts: false,
  bundle: true,
  target: 'es2020',
  metafile: false, // toggle for stats: https://esbuild.github.io/analyze/
  esbuildPlugins: [esbuildPluginVersionInjector()],
  outExtension({ format }) { return { js: `.js` } },
}

const esm: Options = {
  format: ['esm'],
  ...opts,
}

const cjs: Options = {
  format: ['cjs'],
  ...opts,
  platform: "node",
  cjsInterop: true,
  splitting: true,
  outExtension({ format }) { return { js: `.cjs` } },
}

/** Esbuild plugin to stub Node-only funcs for the IIFE build */
const nodeStubPlugin = {
  name: 'node-builtins-stub',
  setup(build: any) {
    const STUB = /^(fs|os|readline|module)$/;
    build.onResolve({ filter: STUB }, (args: any) => ({
      path: args.path, namespace: 'node-stub',
    }));
    build.onLoad({ filter: /.*/, namespace: 'node-stub' }, () => ({
      // let I/O methods fail gracefully at runtime in browser
      contents: `
        export default {};
        export const EOL = '\\n';
        export const createRequire = () => () => ({});
      `,
      loader: 'js',
    }));
  },
};

const iife: Options = {
  format: ['iife'],
  ...opts,
  minify: true,
  platform: "browser",
  globalName: "iife",
  footer: { js: "RiTa = iife.RiTa" },
  outExtension({ format }) { return { js: `.min.js` } },
  esbuildPlugins: [esbuildPluginVersionInjector(), nodeStubPlugin],
}

const testEsm: Options = {
  format: ['esm'],
  platform: "node",
  name: "test",
  entry: ['test/[^i]*.js', '!test/arpabet-ipa.js', '!test/harvard-tests.js'],
  outDir: 'test/dist',
  watch: false,
  clean: false,
  minify: false,
  sourcemap: false,
  dts: false,
  bundle: false,
}

export default defineConfig([esm, cjs, iife, testEsm]);
