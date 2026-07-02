import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
    }).compileComponents();
  });

  it('debería crear la aplicación', () => {
    const fixture = TestBed.createComponent(AppComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });
});
