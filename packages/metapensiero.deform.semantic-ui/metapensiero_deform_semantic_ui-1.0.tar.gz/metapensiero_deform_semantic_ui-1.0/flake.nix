# -*- coding: utf-8 -*-
# :Project:   metapensiero.deform.semantic_ui — Development shell
# :Created:   ven 9 mag 2025, 07:46:45
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2025 Lele Gaifax
#

{
  description = "metapensiero.deform.semantic_ui";

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
        inherit (builtins) fromTOML readFile;
        inherit (gitignore.lib) gitignoreFilterWith;

        pinfo = (fromTOML (readFile ./pyproject.toml)).project;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        pkgs = import nixpkgs { inherit system; };

        pkg = pkgs.python3Packages.buildPythonPackage {
          pname = pinfo.name;
          version = pinfo.version;
          src = getSource "deformantic" ./.;
          pyproject = true;
          build-system = with pkgs.python3Packages; [
            pdm-backend
          ];
          doCheck = false;
          dependencies = with pkgs.python3Packages; [
            deform
            chameleon
          ];
        };

        pydevenv = pkgs.python3.withPackages (ps: [
          pkg
          ps.bump-my-version
          ps.build
          ps.twine
        ]);
      in {
        packages = {
          tinject = pkg;
        };

        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              just
              pydevenv
              twine
            ];

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        };
      });
}
