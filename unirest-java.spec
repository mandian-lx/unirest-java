Summary:	A lightweight HTTP request client libraries for Java
Name:		unirest-java
Version:	1.4.9
Release:	1
License:	MIT
Group:		Development/Java
URL:		https://unirest.io/java.html
Source0:	https://github.com/Mashape/%{name}/archive/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	java-rpmbuild
BuildRequires:	maven-local
BuildRequires:	mvn(org.apache.httpcomponents:httpmime)
BuildRequires:	mvn(org.apache.httpcomponents:httpclient)
BuildRequires:	mvn(org.apache.httpcomponents:httpasyncclient)
BuildRequires:	json
# The followings are required for tests only
BuildRequires:	mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(junit:junit)
BuildRequires:	x11-server-xvfb

Requires:	java-headless
Requires:	mvn(org.apache.httpcomponents:httpmime)
Requires:	mvn(org.apache.httpcomponents:httpclient)
Requires:	mvn(org.apache.httpcomponents:httpasyncclient)
Requires:	json

%description
jsoup is a Java library for working with real-world HTML. It provides
a very convenient API for extracting and manipulating data, using the
best of DOM, CSS, and jquery-like methods.

jsoup implements the WHATWG HTML5 specification (http://whatwg.org/html),
and parses HTML to the same DOM as modern browsers do.

Some features:
  * parse HTML from a URL, file, or string
  * find and extract data, using DOM traversal or CSS selectors
  * manipulate the HTML elements, attributes, and text
  * clean user-submitted content against a safe white-list, to prevent XSS
  * output tidy HTML

jsoup is designed to deal with all varieties of HTML found in the wild; from
pristine and validating, to invalid tag-soup; jsoup will create a sensible
parse tree.

%files -f .mfiles
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{name}-%{version}
# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_add_plugin :maven-jar-plugin . "<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# skip tests requiring a valid connection
%pom_add_plugin :maven-surefire-plugin . "<configuration>
	<excludes>
		<exclude>**/parallelTest*</exclude>
		<exclude>**/testPostRawBody*</exclude>
		<exclude>*testPostRawBody*</exclude>
		<exclude>**/UnirestTest.java</exclude>
	</excludes>
 </configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

