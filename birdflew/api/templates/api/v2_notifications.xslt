<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/notifications">
    <html>
      <head> <title>{{ title }}</title> </head>
      <body>
        <h1>{{ heading }}</h1>
          <xsl:apply-templates select="notification">
            <xsl:sort select="subscription" />
          </xsl:apply-templates>
      </body>
    </html>
  </xsl:template>
 
  <xsl:template match="notification">
    <div class="notification">
     <abbr>
       <xsl:attribute name="class">update</xsl:attribute>
       <xsl:attribute name="title"><xsl:value-of select="update-date" /></xsl:attribute>
       <xsl:value-of select="update-date-formated" />
     </abbr>
     <br/>
     <a>
      <xsl:attribute name="href"><xsl:value-of select="subscription" /></xsl:attribute>
      <xsl:attribute name="rel">subscription</xsl:attribute>Subscription Node
     </a>
     <br/>
     <a>
      <xsl:attribute name="href"><xsl:value-of select="update" /></xsl:attribute>
      <xsl:attribute name="rel">update</xsl:attribute>Updated Bookmark
     </a><br/>
    </div>
  </xsl:template>
 
</xsl:stylesheet>