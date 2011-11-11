<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/users">
    <html>
      <head> <title>{{ title }}</title> </head>
      <body>
        <h1>{{ heading }}</h1>
        <ul class="users">
          <xsl:apply-templates select="user">
            <xsl:sort select="name" />
          </xsl:apply-templates>
        </ul>
      </body>
    </html>
  </xsl:template>
 
  <xsl:template match="user">
    <li class="user">
     <a>
      <xsl:attribute name="href"><xsl:value-of select="link" /></xsl:attribute>
      <xsl:attribute name="rel">details</xsl:attribute><xsl:value-of select="name"/>
     </a>
    </li>
  </xsl:template>
 
</xsl:stylesheet>