Name:           uefistored
Version:        0.4.0
Release:        1%{?dist}
Summary:        Variables store for UEFI guests
License:        GPLv2
URL:            https://github.com/xcp-ng/uefistored
Source0:        https://github.com/xcp-ng/uefistored/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        PK.auth

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libseccomp-devel
BuildRequires:  clang-analyzer
BuildRequires:  git
BuildRequires:  valgrind

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

%build
make

%install
%make_install
# symlink binary to varstored to let XAPI find it
ln -s uefistored %{buildroot}%{_sbindir}/varstored

# Install PK.auth
install -d %{buildroot}%{_datadir}/varstored/
cp %{SOURCE1} %{buildroot}%{_datadir}/varstored/

%check
make -C tests fetch
make test

%files
%{_sbindir}/uefistored
%{_sbindir}/varstored
%dir %{_datadir}/varstored
%{_datadir}/varstored/PK.auth
%{_sbindir}/secureboot-certs

%changelog
* Thu Mar 04 2021 Bobby Eshleman <bobby.eshleman@gmail.com> - 0.4.0-1
- Update to 0.4.0
- Add secureboot-certs script
- Require varstored-tools for secureboot-certs
- Add unit tests to %%check

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
