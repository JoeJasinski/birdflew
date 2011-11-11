<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/user">
    <html>
      <head> <title>{{ title }}</title> </head>
      <body>
        <h1>{{ heading }}</h1>
        <div class="user">
        
          <p>
          <a>
           <xsl:attribute name="href">mailto:<xsl:value-of select="email" /></xsl:attribute>
           <xsl:attribute name="rel">email</xsl:attribute>
           <xsl:value-of select="email" />
          </a>
          </p>

          <p>
          <a>
           <xsl:attribute name="href"><xsl:value-of select="node" /></xsl:attribute>
           <xsl:attribute name="rel">node</xsl:attribute>
           <xsl:value-of select="node" />
          </a>
          </p>

          <p>
          <a>
           <xsl:attribute name="href"><xsl:value-of select="urls" /></xsl:attribute>
           <xsl:attribute name="rel">urls</xsl:attribute>
           <xsl:value-of select="urls" />
          </a>
          </p>
        
        </div>
      </body>
    </html>
  </xsl:template>
 

 
</xsl:stylesheet>