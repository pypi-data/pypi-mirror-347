import { NotebookPanel } from '@jupyterlab/notebook';
import { Cell, MarkdownCell } from '@jupyterlab/cells';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { E2XMarkdownCell } from './cell';
import { IE2xCellPluginRegistry } from './cellplugin';

export class E2XContentFactory extends NotebookPanel.ContentFactory {
  private readonly _settings: ISettingRegistry.ISettings | undefined;
  private readonly _registry: IE2xCellPluginRegistry | undefined;

  constructor(
    options: Cell.ContentFactory.IOptions,
    settings?: ISettingRegistry.ISettings,
    registry?: IE2xCellPluginRegistry
  ) {
    super(options);
    this._settings = settings;
    this._registry = registry;
  }
  createMarkdownCell(options: E2XMarkdownCell.IOptions): MarkdownCell {
    if (!options.contentFactory) {
      options.contentFactory = this;
    }
    options.settings = this._settings;
    options.registry = this._registry;
    const cell = new E2XMarkdownCell(options);
    return cell;
  }
}
