odoo.define('awesome_tshirt.order_kanban_view', function (require) {
    "use strict";

    var core = require('web.core');
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var view_registry = require('web.view_registry');

    var QWeb = core.qweb;


    var OrderKanbanController = KanbanController.extend({
        events: _.extend({}, KanbanController.prototype.events, {
            'click .o_customer': '_onCustomerClicked',
            'input .o_customer_search': '_onCustomerSearchInput',
        }),

        /**
         * @Override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.activeCustomerID = false;
        },
        /**
         * @override
         * @returns {Promise}
         */
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(self._loadCustomers.bind(self));
        },
        /**
         * @override
         */
        start: function () {
            this.$el.addClass('o_order_kanban_view');
            return this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * If a customer is active, sets a domain (used by one of the parent controller)
         * to filter orders for this customer
         * @param params
         * @returns {Promise}
         */
        reload: function (params) {
            if (this.activeCustomerID) {
                params = params || {};
                params.domain = [['customer_id', '=', this.activeCustomerID]];
            }
            return this._super(params).then(this._loadCustomers.bind(this));
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @returns {Promise}
         * @private
         */
        _loadCustomers: function () {
            var self = this;
            return this._rpc({
                route: '/web/dataset/search_read',
                model: 'res.partner',
                fields: ['display_name'],
                domain: [['has_active_order', '=', true]],
            }).then(function (result) {
                self.customers = result.records;
            });
        },
        _update: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_kanban_view').prepend(QWeb.render('OrderKanban.CustomerSidebar', {
                    activeCustomerID: self.activeCustomerID,
                    customers: self.customers,
                }));
            });
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        _onCustomerClicked: function (ev) {
            this.activeCustomerID = $(ev.currentTarget).data('id');
            this.reload();
        },
        _onCustomerSearchInput: function () {
            var self = this;
            var searchVal = this.$('.o_customer_search').val();
            // Find the customers with display_name matching the search box
            var matches = fuzzy.filter(searchVal, _.pluck(this.customers, 'display_name'));
            // Get the indexes for the matching customers
            var indexes = _.pluck(matches, 'index');
            // Map the index back to the customer object in self.customers
            var customers = _.map(indexes, function (index) {
                return self.customers[index];
            });
            // Re-render the customer list and replace the existing ong
            this.$('.o_customer_list').replaceWith(QWeb.render('OrderKanban.CustomerList', {
                activeCustomerID: this.activeCustomerID,
                customers: customers,
            }));
        },
    });

    var OrderKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: OrderKanbanController,
        }),
        display_name: 'Order Kanban',
        icon: 'fa-th-list',
    });

    view_registry.add('order_kanban_view', OrderKanbanView);

});