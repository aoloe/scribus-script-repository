# scribus-script-typographicgrid

Create the typographic grid and the baseline grid based on some parameters for the current page.

http://github.com/aoloe/scribus-script-repository/typographic-grid/

Asks for

- the number of columns
- the size of the main text (in pt; in order to calculate the line height)
- the orientation of the cells

and calculate the cell size and line height that match the grid and still are as close as possible to the values provided.

The script first uses the user's value to calculate
- the number of lines fitting the page
- the width of the columns
- the number of rows fitting in the page that are proportional to the columns

Then
- for ±25% number of rows
- looks for the number of rows that allows a number of lines per page
- with an height that best matches the value based on the font size.

Finally: 
- the line height is adjusted by dividing the page height by the new number of lines,
- the gap is defined,
- the typographic grid created and
- the baseline grid defined


## Notes

- In Scribus' document settings it's possible to set the baseline offset... so we are much more free about how to set the top and bottom margins.

## License:

This program is free software under the MIT license.

Author: Ale Rimoldi <ale@graphicslab.org>

Please report bugs to http://github.com/aoloe/scribus-script-repository/

TODO:

before 1.0:
- implement the API calls for guides columns and rows
- fix the guides columns and rows dialog to show the number of columns and rows instead of the number of guides (starting from 1; leave the sla as is) and use the margin as a default.

further tweaks:
- port to the new scripter and create a real dialog with pyqt
- give the option to avoid reducing the line height
- let the user define a ration between gap and line height (works only for half, double, ... (powers of two))
- let the user define other cells proportions than 2:3

PENDING SCRIBUS BUG REPORTs
- add the setGuidesColumn and setGuidesRow API calls
- fix the doc for the return value of messageBox (cf. comment in this script)


ABOUT THE TYPOGRAPHIC GRID

- http://en.wikipedia.org/wiki/Grid_%28page_layout%29
- http://www.vanseodesign.com/web-design/grid-anatomy/
- http://www.thinkingwithtype.com/contents/grid/
- http://paris.blog.lemonde.fr/2009/02/22/grilles-de-mise-en-page-typographie-web-et-papier/
- http://paris.blog.lemonde.fr/2008/12/27/grilles-de-mise-en-page-typographie-web-et-print/
- http://www.bachgarde.com/gridsystem.html
- http://font.is/grid-systems-making-grids-in-illustrator-2/

Other grid calculators
- http://typedesk.com/2010/12/06/making-grids-with-sigurdur-armannsson-easy-grid-calculator/
  http://font.is/EasyGrid/EasyGridCalculator.htm
  http://font.is/grid-systems-calculate-grids-for-layouts-in-indesign-with-the-help-of-the-easy-grid-calculator/
  http://gridulator.com/

Rules and explanations
- http://www.guylabbe.ca/blog/design-grilles-mise-en-page.html

# Calculate a layout grid with the golden ratio

- http://css.4design.tl/grille-typographique-nombre-d-or/  (french) :

le nombre d'or est de 1.618. (1 + racine carré de 5)/2

on recherche le meilleur rapport entre une largeur optimale et un nombre de colonnes divisible par deux, par trois et/ou par quatre. Les formats composés de 12 ou 24 colonnes répondent à ces critères. (chiffres hautement composé.)

exemple de calcule : largeur de 1024 pixels Pour un document hors marges de 942 pixels : largeur du Viewport moins celle du framework et divisez le résultat par deux pour obtenir la valeur des marges gauche et droite. Exemple : (1 024 – 942) / 2 = 41.

Pour faire entrer ces colonnes dans une largeur donnée, on utilise la gouttière, l’espace séparant les colonnes, comme variable d’ajustement avec des valeurs allant de 10 à 30 pixels.

Pour définir une maquette de magazine destinée à l’impression, nous pouvons partir de la plus petite taille de caractère repérée dans les contenus (notes de bas de page, légendes, etc.) et augmenter la taille des textes en fonction des différents niveaux, (exemple : Notes de bas de page : 8 pt, Légendes des photos : 10 pt, Corps du texte : 12 pt, Intertitres : 14 pt Rubriques  : 18 pt, Titres de Chapitre : 21 pt, Titre de l’ouvrage : 48 pt).

En fonction du style et du public visé par la publication, nous déterminerons ensuite l’empagement à l’aide de tracés régulateurs pour obtenir des blancs tournants (les marges, pour faire simple), puis, pour chaque niveau, nous regarderons le nombre de caractères optimum qui nous donnera la largeur des colonnes, une des clés de la lisibilité et du confort de lecture.

Reste à voir combien de colonnes entreront dans le format dont nous disposons. Dans la plupart des publications, les marges servent de variables d’ajustement ; dans les ouvrages de luxe, c’est le format de l’ouvrage qui peut évoluer pour préserver des blancs tournants généreux.

Et si la seule constante indépassable n’était finalement rien d’autre que l’interlignage ? En effet, s’il y a bien une chose d’un peu scientifique dans le processus de lecture, c’est qu’un interlignage possédant un ratio de 1,5 à 1,6 par rapport à une taille de caractère comprise entre 12 et 16 pixels, possède un potentiel de lisibilité en béton.

une valeur de 21 pixels pour l’interlignage s’est imposée. Ce chiffre correspond à la fois au produit du nombre d’Or typographique par un corps de texte de 14 pixels (1,5 x 14 = 21) et au produit du nombre d’Or tout court par un corps de texte composé en 13 pixels (1,618 x 13 = 21,034), ce qui permet de faire face à la plupart des situations. Un corps de texte en dessous des 13 pixels n’est de toute manière pas très raisonnable !

Il suffit d’utiliser cette valeur pour la gouttière et d’en faire aussi la largeur des colonnes pour obtenir une grille composée uniquement de modules de 21 pixels de large. C’est donc la largeur totale qui devient la variable d’ajustement à la place de la gouttière, permettant à cette dernière d’être en harmonie avec l’interlignage et un regroupement plusieurs colonnes comme 42px + 21px ou 63px + 21px et ainsi de suite.

## infos suplémentaire

Il n'est pas confortable de lire plus de 50 à 60 signes par ligne. Nos yeux se fatiguent à vouloir se forcer à rester sur la même ligne, ils ont tendance à «quitter» la ligne.
