from BeautifulSoup import BeautifulSoup, Tag, NavigableString

def tweak(body):
    soup = BeautifulSoup(body)
    for code_section in soup.findAll('div', attrs={'class' : 'code'}):
        if code_section.text.find('System') > -1:
            language_guess = 'csharp'
        elif code_section.text.find('import') > -1:
            language_guess = 'python'
        elif code_section.text.find('::') > -1:
            language_guess = 'c'
        elif code_section.text.find('</') > -1:
            language_guess = 'html'
        else:
            language_guess = 'javascript'
            
        # Reformat text
        text = ''
        for line in code_section.findAll('pre'):
            if len(line.contents) == 1 and isinstance(line.contents[0], NavigableString):
                text = line.contents[0]
            else:
                stripped = ''.join([x if isinstance(x, NavigableString) else x.text for x in line.contents[1:]])
                text = text + stripped + '\n'
                
        # normalise newlines and stripe the last one
        text = text.replace('\r\n', '\n').strip()
        
        # Build new tags
        code = Tag(soup, 'code', [('data-language', language_guess)])
        code.insert(0, text)
        pre = Tag(soup, 'pre', )
        pre.insert(0, code)
        code_section.replaceWith(pre)

    return str(soup)

if __name__ == '__main__':
    test = """
            <p>If you use .NET, <a href="http://subversion.tigris.org/">Subversion</a> and  <a href="http://nant.sourceforge.net/">NAnt</a> as your personal constellation of  technologies then you've probably found yourself wondering if you can tie the lot  together and have NAnt include your Subversion revision number in as the version  number of your assembly. I've tried a few different approaches over the years and  settled on this one (for now!)</p>
<p>The clever bit of the code (the part which actually grabs the revision number and  gets it into NAnt) has been leeched wholesale from <a href="http://jonathanmalek.com/wp/?p=244">Jonathan Malek</a>,  with the added twist that it creates a C# file with the required attributes in it.</p>
<div class="code">
<pre>&lt;?xml version="1.0"?&gt;
&lt;project name="SetVersion" default="all" basedir="../../"&gt;

    &lt;target name="compile.setversion"&gt;

        &lt;property name="svn.revision" value="0"/&gt;
        &lt;exec
            program="svn"
            commandline='log "${project.src.dir}" --xml --limit 1'
            output="${project.src.dir}\_revision.xml"
            failonerror="true" /&gt;
        &lt;xmlpeek
            file="${project.src.dir}\_revision.xml"
            xpath="/log/logentry/@revision"
            property="svn.revision"
            failonerror="true" /&gt;
        
        &lt;echo file="${project.src.dir}\Version.cs" append="false" message="
            [assembly: System.Reflection.AssemblyVersion("1.0.${svn.revision}")]
            [assembly: System.Reflection.AssemblyFileVersion("${svn.revision}")]" /&gt;
        
    &lt;/target&gt;
&lt;/project&gt;
</pre>
</div>
<p>That sits in its own file. Then, whenever we need to stuff a version number into an assembly  we simply make sure we're including it:</p>
<div class="code">
<pre>&lt;include buildfile="etc/nant/SetVersion.build" /&gt;
</pre>
</div>
<p>and call it just before our csc task:</p>
<div class="code">
<pre>&lt;property name="project.src.dir" value="project/src" /&gt;
&lt;call target="compile.setversion" /&gt;
&lt;csc target="library" output="${out.dir}/${project.name}.dll"&gt;
    &lt;sources&gt;
        &lt;include name="${project.src.dir}/**/*.cs" /&gt;
    &lt;/sources&gt;
&lt;/csc&gt;
</pre>
</div>
<p>Job done!</p>
        """

    print(tweak(test))