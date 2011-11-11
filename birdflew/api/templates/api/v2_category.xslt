<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/categories">
    <html>
      <head> <title>{{ title }}</title> </head>
      <body>
        <h1>{{ heading }}</h1>
          <xsl:apply-templates select="category">
            <xsl:sort select="name" />
          </xsl:apply-templates>
      </body>
    </html>
  </xsl:template>
 
  <xsl:template match="category">
    <div>
     <a>
      <xsl:attribute name="href"><xsl:value-of select="uri" /></xsl:attribute>
      <xsl:attribute name="class">category</xsl:attribute><xsl:value-of select="name"/>
     </a>
    </div>
  </xsl:template>
 
</xsl:stylesheet>