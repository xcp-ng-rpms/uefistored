Name:           uefistored
Version:        1.0.0
Release:        1%{?dist}
Summary:        Variables store for UEFI guests
License:        GPLv2
URL:            https://github.com/xcp-ng/uefistored
Source0:        https://github.com/xcp-ng/uefistored/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        PK.auth
Source2:        https://github.com/nemequ/munit/archive/v0.2.0/munit-0.2.0.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libseccomp-devel
BuildRequires:  clang-analyzer
BuildRequires:  git
BuildRequires:  valgrind
BuildRequires:  libasan

Requires: varstored-guard
Requires: varstored-tools

Obsoletes: varstored

%description
uefistored is a service that runs in dom0 userspace for servicing port
IO RPC requests from the OVMF XenVariable module, thus providing a
protected UEFI Variables Service implementation.

uefistored (the executable is simply uefistored) is started by the XAPI
stack upon running a VM. One running uefistored process exists per HVM
domain start via XAPI.

uefistored uses Xen's libxen to register itself as a device emulator
for the HVM domU that XAPI has started. XenVariable, found in OVMF,
knows how to communicate with uefistored using the device emulation
protocol.

%prep
%autosetup -p1
%setup -a 2

# uefistored expects the munit directory to be at test/munit
ln -sf ../munit-0.2.0 tests/munit

%build
make

%install
%make_install
# symlink binary to varstored to let XAPI find it
ln -s uefistored %{buildroot}%{_sbindir}/varstored

# Install PK.auth
install -d %{buildroot}%{_datadir}/uefistored/
cp %{SOURCE1} %{buildroot}%{_datadir}/uefistored/

# /var/lib/uefistored/ is used by secureboot-certs
install -d %{buildroot}%{_localstatedir}/lib/uefistored/

# varstored-tools expects /usr/share/varstored/ to hold these certificates
install -d %{buildroot}%{_datadir}/varstored/
ln -s %{_datadir}/uefistored/PK.auth %{buildroot}%{_datadir}/varstored/PK.auth
ln -s %{_localstatedir}/lib/uefistored/KEK.auth %{buildroot}%{_datadir}/varstored/KEK.auth
ln -s %{_localstatedir}/lib/uefistored/db.auth %{buildroot}%{_datadir}/varstored/db.auth
ln -s %{_localstatedir}/lib/uefistored/dbx.auth %{buildroot}%{_datadir}/varstored/dbx.auth

%check
make test

%files
%{_sbindir}/uefistored
%{_sbindir}/varstored
%dir %{_datadir}/uefistored
%{_datadir}/uefistored/PK.auth
%{_sbindir}/secureboot-certs
%dir %{_localstatedir}/lib/uefistored

%dir %{_datadir}/varstored
%{_datadir}/varstored/KEK.auth
%{_datadir}/varstored/PK.auth
%{_datadir}/varstored/db.auth
%{_datadir}/varstored/dbx.auth

%changelog
* Thu Jul 01 2021 Bobby Eshleman <bobbyeshleman@gmail.com> - 1.0.0-1
- Update tarball to be that from tag v1.0.0
- Update PK to a more sensible dummy CN

* Thu Jul 01 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-0.1
- Version 1.0.0 with updated secureboot-certs script
- Not based on a tag, so release 0.1, pending the v1.0.0 tag

* Mon May 10 2021 Bobby Eshleman <bobby.eshleman@gmail.com> - 0.6.0-1
- Update to 0.6.0
- Support append writes for uefi variables

* Mon Apr 12 2021 Bobby Eshleman <bobby.eshleman@gmail.com> - 0.5.1-1
- Update to 0.5.1

* Mon Apr 5 2021 Bobby Eshleman <bobby.eshleman@gmail.com> - 0.5.0-1
- Update to 0.5.0
- Add secureboot-certs script
- Require varstored-tools for secureboot-certs
- Add unit tests to %%check
- Add build deps for unit tests
- Create /var/lib/uefistored/ for secureboot-certs
- Add /usr/share/varstored symlinks

* Thu Dec 10 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.3.0-1
- Update to 0.3.0

* Wed Nov 25 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.6-2
- Do not obsolete varstored-tools anymore

* Mon Nov 23 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.6-1
- Update to 0.2.6

* Tue Nov 10 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.5-1
- Update to 0.2.5

* Thu Nov 05 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.4-1
- Update to 0.2.4

* Fri Oct 30 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.3-1
- Update to 0.2.3

* Thu Oct 22 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.2-1
- Update to 0.2.2

* Tue Oct 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.1-1
- Update to 0.2.1

* Fri Aug 21 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1.1-1
- Update to 0.1.1

* Wed Aug 19 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1-1
- Update to 0.1 release of uefistored

* Tue Aug 18 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1-0.pre1.2
- Require varstored-guard

* Thu Aug 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1-0.pre1.1
- Initial build
