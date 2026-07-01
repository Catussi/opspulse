import { Routes } from '@angular/router';

import { PanelOperacionesComponent } from './paginas/panel-operaciones/panel-operaciones.component';

export const routes: Routes = [
  { path: '', component: PanelOperacionesComponent },
  { path: '**', redirectTo: '' },
];
