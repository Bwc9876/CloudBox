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
pkgs.writeScript "cloudbox-backend" ''
  ${pyexe} -m gunicorn cloud_box.wsgi -b 0.0.0.0:8000 &
  ${pyexe} -m webssh.main --port=8001 &
''