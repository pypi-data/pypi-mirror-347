# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext — Development flake
# :Created:   mar 13 mag 2025, 14:23:46
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2025 Lele Gaifax
#

{
  description = "metapensiero.markup.semtext development shell";

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
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        pkg =
          let
            pinfo = (fromTOML (readFile ./pyproject.toml)).project;
          in pkgs.python3Packages.buildPythonPackage {
            pname = pinfo.name;
            version = pinfo.version;
            format = "pyproject";
            src = getSource "semtext" ./.;
            build-system = [ pkgs.python3Packages.pdm-backend ];
            dependencies = with pkgs.python3Packages; [
              lxml
              sly
            ];
          };
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell for mp.markup.semtext";

            packages = (with pkgs; [
              just
              python3
              twine
            ]) ++ (with pkgs.python3Packages; [
              build
              bump-my-version
              pytest
            ]) ++ [ pkg ];

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        };
      });
}
