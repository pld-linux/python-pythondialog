
# NOTE: Python 3 version comes from separate sources

#
# Conditional build:
%bcond_without	doc	# don't build doc

%define 	module	pythondialog
Summary:	Python wrapper for the UNIX "dialog" utility
Name:		python-%{module}
Version:	3.4.0
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
Source0:	http://downloads.sourceforge.net/pythondialog/python2-%{module}-%{version}.tar.bz2
# Source0-md5:	400fd290dd16fbb6beac10b80541ed93
URL:		http://pythondialog.sourceforge.net/
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	dialog
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pythondialog is a Python wrapper for the UNIX dialog utility
originally written by Savio Lam and later rewritten by Thomas E.
Dickey. Its purpose is to provide an easy to use, pythonic and as
complete as possible interface to dialog from Python code.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n python2-%{module}-%{version}

%build
%py_build

%if %{with doc}
cd doc
%{__make} -j1 html SPHINXBUILD=sphinx-build-2
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install
%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst TODO
%{py_sitescriptdir}/dialog.*
%{py_sitescriptdir}/python2_%{module}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif
