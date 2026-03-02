import {getMovistarSkin} from '@telefonica/mistica';

export const misticaTheme = {
  skin: getMovistarSkin(),
  i18n: {locale: 'pt-BR' as const, phoneNumberFormattingRegionCode: 'BR' as const},
};
