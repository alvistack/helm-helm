# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: helm
Epoch: 100
Version: 3.15.2
Release: 1%{?dist}
Summary: Kubernetes Package Manager
License: Apache-2.0
URL: https://github.com/helm/helm/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.23
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
            -X helm.sh/helm/v3/internal/version.gitCommit='3fc9f4b2638e76f26739cd77c7017139be81d0ea' \
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
