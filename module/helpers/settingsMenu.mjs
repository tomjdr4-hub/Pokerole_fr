const { ApplicationV2, HandlebarsApplicationMixin } = foundry.applications.api;

export class ailmentsMenu extends HandlebarsApplicationMixin(ApplicationV2) {
  static DEFAULT_OPTIONS = {
    id: 'pokerole-ailments',
    classes: ['pokerole'],
    window: {
      title: "Ailment Settings",
      resizable: true,
    },
    position: {
      width: 500,
      height: 'auto',
    }
  };

  static PARTS = {
    form: {
      template: 'systems/pokerole/templates/settings/settings-ailments.hbs'
    }
  };

  async _prepareContext(_options) {
    return {
      burnSTR: game.settings.get('pokerole', 'burnConst'),
      frozenSPE: game.settings.get('pokerole', 'frozenConst'),
      paralysisDEX: game.settings.get('pokerole', 'paralysisConst')
    };
  }

  _onRender(_context, _options) {
    this.element.querySelectorAll('input[type="number"]').forEach(input => {
      input.addEventListener('change', function(event) {
        event.preventDefault();
        const { id } = event.target.dataset;
        if (id) game.settings.set('pokerole', id, Number(event.target.value));
      });
    });
  }
}
