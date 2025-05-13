*   Tag commit the result with a version number

        git tag -a x.x.x -m 'Version x.x.x'

*   and push to github

        git push origin master --tags

*  Verify the version number is correct

        pixi r -e build get_version
        0.1.22

        # if it contains .dev, you can always override before building with:
        export SETUPTOOLS_SCM_PRETEND_VERSION=0.1.21

*   Build the source distribution locally
    
        pixi r -e build build

*  Upload to PyPI

        pixi r -e build upload