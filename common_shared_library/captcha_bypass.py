from anticaptchaofficial.recaptchav2proxyless import *
import os
from dotenv import load_dotenv
import logging

load_dotenv(verbose=True, override=True)

ANTICAPTCHA_KEY = os.getenv('ANTICAPTCHA_KEY')

logger = logging.getLogger(__name__)

class CaptchaBypass(object):
    def __init__(self, sitekey, url):
        self.sitekey = sitekey
        self.url = url

    def bypass(self):

        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(ANTICAPTCHA_KEY)
        solver.set_website_url(self.url)
        solver.set_website_key(self.sitekey)

        g_response = solver.solve_and_return_solution()
        if g_response == 0:
            # print(f"task finished with error: {solver.error_code}")
            logger.error(f"task finished with error: {solver.error_code}")
        else:
            # print(f"Captcha Response generated: {str(g_response)}")
            logger.info(f"Captcha Response generated: *****{str(g_response)[:-5]}")

        return g_response
