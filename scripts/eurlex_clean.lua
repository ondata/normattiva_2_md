-- Clean EUR-Lex XHTML when converting to Markdown.

local function has_class(el, class)
  local classes = el.classes or (el.attr and el.attr.classes) or {}
  for _, c in ipairs(classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function blocks_to_inlines(blocks)
  return pandoc.utils.blocks_to_inlines(blocks)
end

local function table_text(el)
  return pandoc.utils.stringify(el)
end

local function normalize_space(s)
  return s:gsub("\194\160", " ")
end

local function trim(s)
  return (s:gsub("^%s+", ""):gsub("%s+$", ""))
end

local function is_single_letter(s)
  return s and s:match("^[a-z]$") ~= nil
end

local function is_considerando(s)
  return s:match("^%(%d+%)%s")
end

function Div(el)
  local classes = el.classes or (el.attr and el.attr.classes) or {}
  if #classes == 0 then
    return el.content
  end
  if has_class(el, "eli-container") or has_class(el, "eli-subdivision") then
    return el.content
  end
  if has_class(el, "oj-final") or has_class(el, "oj-signatory") then
    return el.content
  end

  if has_class(el, "eli-main-title") then
    local blocks = {}
    local first = nil
    for _, b in ipairs(el.content) do
      if b.t == "Para" or b.t == "Plain" then
        if not first then
          first = b
        else
          table.insert(blocks, pandoc.Para(b.content))
        end
      end
    end
    if first then
      table.insert(blocks, 1, pandoc.Header(1, first.content))
      return blocks
    end
  end

  if has_class(el, "eli-title") then
    local level = 3
    if el.identifier and el.identifier:match("^cpt_") then
      level = 3
    elseif el.identifier and el.identifier:match("^art_") then
      level = 4
    end
    local inlines = blocks_to_inlines(el.content)
    return pandoc.Header(level, inlines)
  end
end

function Para(el)
  local classes = el.classes or (el.attr and el.attr.classes) or {}
  for _, c in ipairs(classes) do
    if c == "oj-ti-section-1" then
      return pandoc.Header(2, el.content)
    end
    if c == "oj-ti-art" then
      return pandoc.Header(3, el.content)
    end
  end
  local text = normalize_space(pandoc.utils.stringify(el))
  if text:match("^CAPO%s+%d+") and text:match("^CAPO%s+%d+%s*$") then
    return pandoc.Header(2, el.content)
  end
  if text:match("^Articolo%s+%d+%s*$") then
    local h = pandoc.Header(3, el.content)
    h.attr.attributes = h.attr.attributes or {}
    h.attr.attributes["data-article"] = "true"
    return h
  end
  if is_considerando(text) then
    return pandoc.Div({pandoc.Para(el.content)}, pandoc.Attr("", {"considerando"}))
  end
end

function Plain(el)
  local classes = el.classes or (el.attr and el.attr.classes) or {}
  for _, c in ipairs(classes) do
    if c == "oj-ti-section-1" then
      return pandoc.Header(2, el.content)
    end
    if c == "oj-ti-art" then
      return pandoc.Header(3, el.content)
    end
  end
  local text = normalize_space(pandoc.utils.stringify(el))
  if text:match("^CAPO%s+%d+") and text:match("^CAPO%s+%d+%s*$") then
    return pandoc.Header(2, el.content)
  end
  if text:match("^Articolo%s+%d+%s*$") then
    local h = pandoc.Header(3, el.content)
    h.attr.attributes = h.attr.attributes or {}
    h.attr.attributes["data-article"] = "true"
    return h
  end
  if is_considerando(text) then
    return pandoc.Div({pandoc.Para(el.content)}, pandoc.Attr("", {"considerando"}))
  end
end

function Table(el)
  local text = table_text(el)
  if text:find("Gazzetta ufficiale") or text:find("Serie L") or text:find("European flag") then
    return {}
  end

  local cols = #el.colspecs
  if cols >= 3 then
    local has_alpha = text:match("%a")
    local has_date = text:match("%d%d?%.%d%d?%.%d%d%d%d")
    if not has_alpha and has_date then
      return {}
    end
  end
  if cols ~= 2 or #el.bodies ~= 1 then
    return nil
  end
  local body = el.bodies[1]
  if #body.body ~= 1 then
    return nil
  end
  local row = body.body[1]
  if #row.cells ~= 2 then
    return nil
  end

  local cell1 = row.cells[1].contents
  local cell2 = row.cells[2].contents
  local inlines1 = blocks_to_inlines(cell1)
  local inlines2 = blocks_to_inlines(cell2)

  local left = trim(normalize_space(pandoc.utils.stringify(pandoc.Plain(inlines1))))
  local left_letter = left:match("^(%a)%)$")
  if left_letter then
    local right = pandoc.List()
    right:insert(pandoc.Str(left))
    right:insert(pandoc.Space())
    for _, v in ipairs(inlines2) do
      right:insert(v)
    end
    return pandoc.BulletList({{pandoc.Para(right)}})
  end

  if left:match("^%(%d+%)$") then
    return pandoc.Div({pandoc.Para(inlines2)}, pandoc.Attr("", {"considerando"}))
  end

  local out = pandoc.List()
  for _, v in ipairs(inlines1) do
    out:insert(v)
  end
  out:insert(pandoc.Space())
  for _, v in ipairs(inlines2) do
    out:insert(v)
  end

  return pandoc.Para(out)
end

function RawBlock(el)
  if el.format == "html" then
    if el.text:match("^%s*<div") or el.text:match("^%s*</div") then
      return {}
    end
    if el.text:match("^%s*<!--") then
      return {}
    end
  end
end

function HorizontalRule(el)
  return {}
end

function Span(el)
  if has_class(el, "oj-bold") or has_class(el, "oj-super") or has_class(el, "oj-note-tag") then
    return el.content
  end
end

function Link(el)
  return pandoc.Link(el.content, el.target, el.title)
end

function Header(el)
  if el.level == 3 and el.content then
    local text = normalize_space(pandoc.utils.stringify(el))
    if text:match("^Articolo%s+%d+%s*$") then
      el.attr.attributes = el.attr.attributes or {}
      el.attr.attributes["data-article"] = "true"
    end
  end
  return el
end

function Pandoc(doc)
  local out = pandoc.List()
  local pending_article = nil
  local in_considerando = false
  local considerandi = pandoc.List()

  local function flush_considerandi()
    if #considerandi > 0 then
      out:insert(pandoc.OrderedList(considerandi))
      considerandi = pandoc.List()
    end
  end

  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 3 then
      if b.attr and b.attr.attributes and b.attr.attributes["data-article"] == "true" then
        if pending_article then
          out:insert(pending_article)
        end
        pending_article = b
        flush_considerandi()
        in_considerando = false
        goto continue
      end
    end

    if pending_article and b.t == "Header" and b.level == 4 then
      local title = normalize_space(pandoc.utils.stringify(b))
      if #pending_article.content > 0 then
        pending_article.content:insert(pandoc.Space())
        pending_article.content:insert(pandoc.Str("-"))
        pending_article.content:insert(pandoc.Space())
        pending_article.content:insert(pandoc.Str(title))
      end
      out:insert(pending_article)
      pending_article = nil
      goto continue
    end

    if pending_article and (b.t ~= "Header") then
      out:insert(pending_article)
      pending_article = nil
    end

    if b.t == "Div" and has_class(b, "considerando") then
      considerandi:insert(b.content)
      in_considerando = true
      goto continue
    end

    if in_considerando then
      flush_considerandi()
      in_considerando = false
    end

    out:insert(b)
    ::continue::
  end

  if pending_article then
    out:insert(pending_article)
  end
  flush_considerandi()

  doc.blocks = out
  return doc
end
