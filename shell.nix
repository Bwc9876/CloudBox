{pkgs ? import <nixpkgs> {} }:
let
  python = pkgs.python3.withPackages (ps: with ps; [
    django
    webssh
    paramiko
    google-cloud-compute
    gunicorn
  ]);
  pyexe = pkgs.lib.getExe python;
in
python.env