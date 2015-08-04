from tethys_apps.base import TethysAppBase, url_map_maker


class WpsTester(TethysAppBase):
    """
    Tethys app class for WPS Tester.
    """

    name = 'WPS Tester'
    index = 'wps_tester:home'
    icon = 'wps_tester/images/icon.gif'
    package = 'wps_tester'
    root_url = 'wps-tester'
    color = '#3498db'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='wps-tester',
                           controller='wps_tester.controllers.home'),
        )

        return url_maps