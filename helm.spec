%global debug_package %{nil}

Name: helm
Epoch: 100
Version: 3.9.0
Release: 1%{?dist}
Summary: Kubernetes Package Manager
License: Apache-2.0
URL: https://github.com/helm/helm/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static

%description
Helm is a tool for managing Charts. Charts are packages of
pre-configured Kubernetes resources.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm' \
            -X helm.sh/helm/v3/internal/version.gitCommit='7ceeda6c585217a19a1131663d8cd1f7d641b2a7' \
            -X helm.sh/helm/v3/internal/version.gitTreeState='clean' \
        " \
        -o ./bin/helm ./cmd/helm

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/helm

%files
%license LICENSE
%{_bindir}/*

%changelog
