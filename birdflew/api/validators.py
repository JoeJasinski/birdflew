from lxml import etree

input_message_spec = """<element name="urls" xmlns="http://relaxng.org/ns/structure/1.0">
  <oneOrMore>
    <element name="url">
      <text/>
    </element>
  </oneOrMore>
</element>
"""

def input_message_spec_relaxing():
    xml = etree.fromstring(input_message_spec)
    return etree.RelaxNG(xml)