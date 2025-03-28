###
# Copyright (c) 2005, Jeremiah Fincher
# Copyright (c) 2010-2021, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import re

import supybot.conf as conf
import supybot.registry as registry
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('ChannelStats')

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('ChannelStats', True)

class Smileys(registry.Value):
    def __init__(self, *args, **kwargs):
        self.s = ''
        super().__init__(*args, **kwargs)

    def set(self, s):
        L = s.split()
        self.setValue(L)

    def setValue(self, v):
        self._lastModified = registry.monotonic_time()
        self.s = ' '.join(v)
        self.value = re.compile('|'.join(map(re.escape, v)))

    def __str__(self):
        return self.s

ChannelStats = conf.registerPlugin('ChannelStats')
conf.registerChannelValue(ChannelStats, 'selfStats',
    registry.Boolean(True, _("""Determines whether the bot will keep channel
    statistics on itself, possibly skewing the channel stats (especially in
    cases where the bot is relaying between channels on a network).""")))
conf.registerChannelValue(ChannelStats, 'smileys',
    Smileys(':) ;) ;] :-) :-D :D :P :p (= =)'.split(), _("""Determines what
    words (i.e., pieces of text with no spaces in them) are considered
    'smileys' for the purposes of stats-keeping.""")))
conf.registerChannelValue(ChannelStats, 'frowns',
    Smileys(':| :-/ :-\\ :\\ :/ :( :-( :\'('.split(), _("""Determines what words
    (i.e., pieces of text with no spaces in them) are considered 'frowns' for
    the purposes of stats-keeping.""")))

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
