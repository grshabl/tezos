%define tezos_prefix /opt/tezos

Name:		tezos
Version:	0.1
Release:	1%{?dist}
Summary:	tezos

Group:		crypto
License:	proprietary
URL:		https://www.tezos.com/

ExclusiveArch: x86_64

Source0: ./tezos-prebuilt.tar

BuildRequires: patchelf

Requires: glibc
Requires: gmp
Requires: libgcc
Requires: libstdc++
Requires: snappy
Requires: compat-openssl10
Requires: leveldb


%description


%build
%prep
%setup -n tezos

# nix built stuff is "immutable"
chmod 755 ./tezos-node

patchelf --set-rpath "%{_libdir}" \
         --replace-needed libssl.so.1.0.0 libssl.so.10 \
         --replace-needed libcrypto.so.1.0.0 libcrypto.so.10 \
         --set-interpreter "$(patchelf --print-interpreter "%{__ld}")" \
         ./tezos-node

# patchbash?
sed -i '1s@#![[:space:]]*/nix/store/[^/]*/bin@%{_bindir}@' ./tezos-sandboxed-node.sh
sed -i '1s@#![[:space:]]*/nix/store/[^/]*/bin@%{_bindir}@' ./tezos-init-sandboxed-client.sh
# ldd ./tezos-node
# head ./tezos-sandboxed-node.sh

%install
mkdir -p ${RPM_BUILD_ROOT}%{tezos_prefix}/bin
cp -p %{_builddir}/tezos/tezos-node                     ${RPM_BUILD_ROOT}%{tezos_prefix}/bin/tezos-node
cp -p %{_builddir}/tezos/tezos-sandboxed-node.sh        ${RPM_BUILD_ROOT}%{tezos_prefix}/bin/tezos-sandboxed-node.sh
cp -p %{_builddir}/tezos/tezos-client                   ${RPM_BUILD_ROOT}%{tezos_prefix}/bin/tezos-client
cp -p %{_builddir}/tezos/tezos-admin-client             ${RPM_BUILD_ROOT}%{tezos_prefix}/bin/tezos-admin-client
cp -p %{_builddir}/tezos/tezos-init-sandboxed-client.sh ${RPM_BUILD_ROOT}%{tezos_prefix}/bin/tezos-init-sandboxed-client.sh


%files

%{tezos_prefix}/*

%changelog

