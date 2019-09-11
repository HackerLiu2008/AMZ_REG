# 获取geosurf代理ip的方法
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pluginPath = 'C:/vimm_chrome_proxyauth_plugin.zip'


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension

    args:
      proxy_host (str): domain or ip address, ie proxy.domain.com
      proxy_port (int): port
      proxy_username (str): auth username
      proxy_password (str): auth password
    kwargs:
      scheme (str): proxy scheme, default http
      plugin_path (str): absolute path of the extension

    return str -> plugin_path
    """
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = pluginPath

    manifest_json = """
  {
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
      "proxy",
      "tabs",
      "unlimitedStorage",
      "storage",
      "<all_urls>",
      "webRequest",
      "webRequestBlocking"
    ],
    "background": {
      "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
  }
  """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
              scheme: "${scheme}",
              host: "${host}",
              port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
            };
      
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
      
        function callbackFn(details) {
          return {
            authCredentials: {
              username: "${username}",
              password: "${password}"
            }
          };
        }
      
        chrome.webRequest.onAuthRequired.addListener(
              callbackFn,
              {urls: ["<all_urls>"]},
              ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def getpro():
    co = Options()
    customer_id = '9071'
    location = 'FR'
    session_number = random.randint(200000, 400000)
    user_name = '{}+{}+{}'.format(customer_id, location, session_number)

    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=location + "-10m.geosurf.io",
        proxy_port=8000,
        proxy_username=user_name,
        proxy_password="t8e1baj2y"
    )
    co.add_extension(proxyauth_plugin_path)
    prefs = {'profile.managed_default_content_settings.images': 2}
    co.add_experimental_option('prefs', prefs)
    co.add_argument('disable-infobars')
    # co.add_argument('--headless')
    # co.add_argument('--disable-gpu')

    # 验证代理是否有效，无效则重新生成
    dr = webdriver.Chrome(options=co)
    url_ip_info = 'http://geo.geosurf.io/'
    # 获取代理ip信息

    dr.set_page_load_timeout(5)
    try:
        dr.get(url_ip_info)
        page_source = dr.page_source
        if 'pre-wrap;">{"ip' in page_source:
            dr.quit()
            return co
        else:
            dr.quit()
            getpro()
    except:
        dr.quit()
        getpro()

