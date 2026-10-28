// Sjabloon: een foutformaat met stabiele codes (application/problem+json, RFC 9457).
// Dekt: API-11, API-10
// Aanpassen: de lijst codes. Zet nooit een stack, query, bestandspad of intern id in een fout (API-11).
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.

export interface Problem {
  type: string;
  title: string;
  status: number;
  code: string;
  req_id?: string;
}

// Een fout die je bewust gooit en die de client mag zien.
export class AppError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, titel: string) {
    super(titel);
    this.status = status;
    this.code = code;
  }

  toProblem(reqId: string): Problem {
    return { type: 'about:blank', title: this.message, status: this.status, code: this.code, req_id: reqId };
  }
}

// Vaste, algemene titels voor fouten die je niet zelf gooit. De tekst van de echte fout gaat alleen naar het log.
export const ALGEMEEN: Record<number, string> = {
  400: 'Ongeldige invoer',
  401: 'Niet ingelogd',
  403: 'Geen toegang',
  404: 'Niet gevonden',
  409: 'Verzoek loopt al',
  413: 'Verzoek te groot',
  415: 'Dit type inhoud wordt niet geaccepteerd',
  429: 'Te veel verzoeken',
  500: 'Er ging iets mis',
};
