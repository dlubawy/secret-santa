{
  description = "A Nix flake based Node environment";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/release-24.05";

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        f: nixpkgs.lib.genAttrs supportedSystems (system: f { pkgs = import nixpkgs { inherit system; }; });
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default = pkgs.mkShell {
            venvDir = "venv";
            packages = with pkgs; [
              black
              firebase-tools
              isort
              node2nix
              nodePackages_latest.eslint
              nodePackages_latest.prettier
              nodejs
              openjdk
              python311
              yarn
            ] ++ (with pkgs.python311Packages; [
              pip
              venvShellHook
            ]);
            env = {
              shell = "zsh";
            };
          };
        }
      );
    };
}
