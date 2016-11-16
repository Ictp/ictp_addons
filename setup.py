from setuptools import setup, find_packages
if __name__ == '__main__':
    setup(
        name='ictp_addons',
        version="0.7",
        description="Ictp useful tools",
        author="Giorgio Pieretti",
        packages=find_packages(),
        include_package_data=True,
        install_requires=[],
        package_dir={'ictp_addons': 'ictp_addons'},
        entry_points="""
            [indico.ext_types]
            ictp_addons = indico.ext.ictp_addons

            [indico.ext]
            ictp_addons.sponsor_management = indico.ext.ictp_addons.sponsor_management
            ictp_addons.poster_management = indico.ext.ictp_addons.poster_management
	        ictp_addons.custompage_management = indico.ext.ictp_addons.custompage_management
        """
    )

