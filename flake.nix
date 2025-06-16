{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    # Last working commit from nixos-small-unstable
    nixpkgs.url = "github:NixOS/nixpkgs?rev=75e28c029ef2605f9841e0baa335d70065fe7ae2";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        myapp = { poetry2nix, lib }: poetry2nix.mkPoetryApplication {
          projectDir = self;
          overrides = poetry2nix.overrides.withDefaults (final: super:
            lib.mapAttrs
              (attr: systems: super.${attr}.overridePythonAttrs
                (old: {
                  nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ map (a: final.${a}) systems;
                }))
              {
                # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md#modulenotfounderror-no-module-named-packagename
                # package = [ "setuptools" ];
              }
          );
        };
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            poetry2nix.overlays.default
            (final: _: {
              myapp = final.callPackage myapp { };
            })
          ];
        };
      in
      {
        packages.default = pkgs.myapp;
        devShells = {
          # Shell for app dependencies.
          #
          #     nix develop
          #
          # Use this shell for developing your app.
          default = pkgs.mkShell {
            inputsFrom = [ pkgs.myapp ];
          };

          # Shell for poetry.
          #
          #     nix develop .#poetry
          #
          # Use this shell for changes to pyproject.toml and poetry.lock.
          poetry = pkgs.mkShell {
            packages = [ pkgs.poetry ];
          };
        };
        legacyPackages = pkgs;
      }
    );
}
