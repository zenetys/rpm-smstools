# Supported targets: el9

Name: smstools
Version: 3.1.21
Release: 1%{?dist}.zenetys
Summary: Send and receive SMS through GSM modems or mobile phones
Group: Applications/Communications
License: GPLv2+
URL: http://smstools3.kekekasvi.com

Source0: http://smstools3.kekekasvi.com/packages/smstools3-%{version}.tar.gz
Source1: smsd.logrotate
Source2: smsd.tmpfiles
Source3: smsd.service

BuildRequires: gcc
BuildRequires: systemd

%description
The SMS Server Tools 3 is a SMS Gateway software which can send and
receive short messages through GSM modems and mobile phones.

%prep
%setup -n smstools3

%build
make -C src \
    'CFLAGS=%{build_cflags} -DNOSTATS -DNUMBER_OF_MODEMS=64 -fcommon' \
    'LFLAGS=%{build_ldflags}' \
    %{?_smp_mflags}

%install
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/logrotate.d/smsd
install -D -m 0640 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/smsd.conf
install -D -m 0644 %{SOURCE3} %{buildroot}/%{_unitdir}/smsd.service
install -D -m 0640 examples/smsd.conf.easy %{buildroot}/%{_sysconfdir}/smsd.conf
install -D -m 0755 src/smsd %{buildroot}/%{_sbindir}/smsd
install -D -m 0755 scripts/sendsms %{buildroot}/%{_bindir}/smssend
install -D -m 0755 scripts/sms2html %{buildroot}/%{_bindir}/sms2html
install -D -m 0755 scripts/sms2unicode %{buildroot}/%{_bindir}/sms2unicode
install -D -m 0755 scripts/sms2xml %{buildroot}/%{_bindir}/sms2xml
install -D -m 0755 scripts/unicode2sms %{buildroot}/%{_bindir}/unicode2sms
install -D -d -m 0750 %{buildroot}/%{_localstatedir}/spool/sms/checked
install -D -d -m 0750 %{buildroot}/%{_localstatedir}/spool/sms/failed
install -D -d -m 0750 %{buildroot}/%{_localstatedir}/spool/sms/incoming
install -D -d -m 0770 %{buildroot}/%{_localstatedir}/spool/sms/outgoing
install -D -d -m 0750 %{buildroot}/%{_localstatedir}/spool/sms/sent
install -D -d -m 0750 %{buildroot}/%{_localstatedir}/log/smsd
install -D -d -m 0755 %{buildroot}/%{_rundir}/smsd

%pre
if ! getent group smsd > /dev/null; then
    groupadd -r smsd
fi
if ! getent passwd smsd > /dev/null; then
    useradd -r -g smsd -G dialout -d %{_localstatedir}/spool/sms -s /sbin/nologin smsd
fi

%post
%systemd_post smsd.service

%preun
%systemd_preun smsd.service

%postun
%systemd_postun_with_restart smsd.service

%files
%defattr(-, root, root, -)

%doc doc/*
%license LICENSE

%config(noreplace) %{_sysconfdir}/logrotate.d/smsd
%config(noreplace) %attr(-, -, smsd) %{_sysconfdir}/smsd.conf

%{_bindir}/*
%{_sbindir}/*
%{_tmpfilesdir}/smsd.conf
%{_unitdir}/smsd.service

%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/
%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/checked
%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/failed
%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/incoming
%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/outgoing
%attr(-, smsd, smsd) %dir %{_localstatedir}/spool/sms/sent
%attr(-, smsd, smsd) %dir %{_localstatedir}/log/smsd
%attr(-, smsd, smsd) %ghost %{_localstatedir}/log/smsd.log
%attr(-, smsd, smsd) %dir %{_rundir}/smsd
