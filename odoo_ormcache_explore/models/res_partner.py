# Copyright 2021 Raman K.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.tools import ormcache, ormcache_context
from odoo import models, fields

import logging


_log = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    occupation = fields.Char(
        string='Occupation',
    )
    occupation_info = fields.Char(
        string='Occupation Info',
    )
    lru_cache = fields.Text(
        string='LRU Cache',
    )
    lru_cache_len = fields.Integer(
        string='Cache Len',
    )
    filter_names = fields.Char(
        string='Filter',
    )

    def _format_lru_cache_to_text(self, apply_filter):
        _log.info('_format_lru_cache_to_text method!')

        lru_dict = self.pool._Registry__cache.d  # self.env.registry._Registry__cache.d

        if apply_filter:
            names = self.filter_names.split(',')
            to_list = ['%s : %s' % (k, v) for k, v in lru_dict.items() if k[0] in names]
        else:
            to_list = ['%s : %s' % (k, v) for k, v in lru_dict.items()]

        return len(lru_dict), '\n\n'.join(to_list)

    # @ormcache_context('occupation', keys=('ctx_variable',))
    # @ormcache('occupation', 'self.name')
    @ormcache()
    def _get_occupation_info(self, occupation):
        _log.info('_get_occupation_info method!')

        return 'The greatest %s %s' % (occupation, self.name)

    def get_occupation_info(self):

        # info = self.with_context(ctx_variable=self.filter_names)\
        #     ._get_occupation_info(self.occupation)

        info = self._get_occupation_info(self.occupation)

        self.write({
            'occupation_info': info,
        })

    def clear_lru_cache_field(self):

        self.write({
            'lru_cache': False,
            'lru_cache_len': False,
            'occupation_info': False,
        })

    def get_lru_cache(self):

        lru_cache_len, lru_cache_text = self._format_lru_cache_to_text(
            self.env.context.get('apply_filter'),
        )
        self.write({
            'lru_cache': lru_cache_text,
            'lru_cache_len': lru_cache_len,
        })

    def clear_lru_cache(self):
        self.__class__.clear_caches()
