# -*- coding: utf-8 -*-
# :Project:   metapensiero.sphinx.autodoc_sa — Development flake
# :Created:   gio 23 giu 2022, 15:33:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2025 Lele Gaifax
#

{
  description = "metapensiero.sphinx.autodoc_sa development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML getAttr listToAttrs map readFile replaceStrings;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) cartesianProduct;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # Python versions to test against: "python3" is the current major version
        # in NixOS
        pyVersions = [
          "python3"
          # "python39"
          # "python310"
          # "python311"
        ];

        # SQLAlchemy versions to try out
        saVersions = [
          { version = "1.4.54";
            hash = "sha256-RHD77QiMNdwgt4o5qvSuVP6BeQx4OzJkhyoCJPQ3wxo="; }
          { version = "2.0.40";
            hash = "sha256-2CcJkonGRYlBjrvK6tAUXNGfTj6Kk5GaAQAkevJF+gA="; }];

        mkSAPkg = python: saVersion:
          python.pkgs.buildPythonPackage rec {
            pname = "sqlalchemy";
            version = saVersion.version;
            src = python.pkgs.fetchPypi {
              inherit pname version;
              hash = saVersion.hash;
            };
            doCheck = false;
            nativeBuildInputs = [ python.pkgs.cython ];
            propagatedBuildInputs = [
              python.pkgs.greenlet
              python.pkgs.typing-extensions
            ];
          };

        mkPkg = pyVersion: saVersion: doCheck:
          let
            py = getAttr pyVersion pkgs;
            sqlalchemy' = mkSAPkg py saVersion;
            pinfo = (fromTOML (readFile ./pyproject.toml)).project;
          in py.pkgs.buildPythonPackage {
            inherit doCheck;
            pname = "${pinfo.name}-${saVersion.version}";
            version = pinfo.version;
            format = "pyproject";
            src = getSource "autodoc_sa" ./.;
            checkPhase = "pytest";
            checkInputs = with py.pkgs; [
              pglast
              pytest
              sphinx
              sqlalchemy'
            ];
            nativeBuildInputs = with py.pkgs; [
              pdm-backend
            ];
            propagatedBuildInputs = with py.pkgs; [
              progressbar2
              ruamel-yaml
              sphinx
              sqlalchemy'
            ];
          };

        checkPkgs = map
          (combo: mkPkg combo.pyv combo.sav true)
          (cartesianProduct { pyv = pyVersions; sav = saVersions; });

        mkTestShell = pyVersion: saVersion:
          let
            py = getAttr pyVersion pkgs;
            pkg = mkPkg pyVersion saVersion false;
            env = py.buildEnv.override {
              extraLibs = [
                pkg
                py.pkgs.pglast
                py.pkgs.pytest
              ];
            };
          in pkgs.mkShell {
            name = "py-${py.version}+sa-${saVersion.version}";
            packages = with pkgs; [
              bump-my-version
              just
              env
            ];
          };

        testShells = map
          (combo: mkTestShell combo.pyv combo.sav)
          (cartesianProduct { pyv = pyVersions; sav = saVersions; });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell for mp.sphinx.autodoc_sa";

            packages = (with pkgs; [
              bump-my-version
              just
              python3
              twine
            ]) ++ (with pkgs.python3Packages; [
              build
              bump-my-version
              pglast
              pytest
              sphinx
              sqlalchemy
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        } // (listToAttrs (map (s: {
          name = replaceStrings ["."] ["_"] s.name;
          value = s;
        }) testShells));

        checks = listToAttrs (map (p: {
          name = replaceStrings ["."] ["_"] p.name;
          value = p;
        }) checkPkgs);
      });
}
