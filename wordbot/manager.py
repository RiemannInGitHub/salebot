import salebot

from util import log

logger = log.get_logger(__name__)


# TODO: auto delete bot while no using after 10 min
class Manager(object):
    def __init__(self):
        self.salebotlist = []

    def create_bot(self, userid):
        bot = salebot.SaleBot(userid)
        self.salebotlist.append(bot)
        logger.info("[MANAGER]the bot of userid:" + userid + " has been created")
        return bot

    def get_bot(self, userid):
        for bot in self.salebotlist:
            if bot.user.userid == userid:
                logger.info("[MANAGER]get bot userid:" + userid)
                return bot
        logger.warning("[MANAGER]userid:" + userid + "don't has a bot yet")
        return None

    def get_create_bot(self, userid):
        for bot in self.salebotlist:
            if bot.user.userid == userid:
                logger.info("[MANAGER]get bot userid:" + userid)
                return bot
        bot = self.create_bot(userid)
        return bot

    def del_bot(self, userid):
        for bot in self.salebotlist:
            if bot.user.userid == userid:
                self.salebotlist.remove(bot)
                del bot
                logger.info("[MANAGER]the bot of userid:" + userid + " has been deleted")
                return True
        logger.warning("[MANAGER]there is no bot belong to userid " + userid)
        return False

