{
  description = "VarChamp Batch-13 image QC tooling — Nix provides the pixi binary, pixi manages the Python scientific stack";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "aarch64-darwin";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.pixi ];
        shellHook = ''
          echo "VarChamp QC shell. First time: pixi install"
          echo "Then:            pixi run edit   # open the marimo picker notebook"
        '';
      };
    };
}
