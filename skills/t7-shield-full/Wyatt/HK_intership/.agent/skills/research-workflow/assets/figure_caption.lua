local chapter = 0
local fig = 0

local function url_decode(s)
  return s and s:gsub("%%(%x%x)", function(h) return string.char(tonumber(h,16)) end) or s
end
local function file_exists(path)
  local f = io.open(path, "rb")
  if f then f:close() return true end
  return false
end
local root = nil
local function ensure_root()
  if not root then
    local inputs = PANDOC_STATE and PANDOC_STATE.input_files or nil
    if inputs and #inputs > 0 then
      root = pandoc.path.directory(inputs[1])
    else
      root = "."
    end
  end
end

local function make_caption_inlines(text)
  -- 如果未能正确识别章节号(chapter=0)，则默认为第2章
  local effective_chapter = (chapter == 0) and 2 or chapter
  local prefix = string.format("图 %d-%d ", effective_chapter, fig)
  return { pandoc.Str(prefix), pandoc.Str(text) }
end

function Image(img)
  if img.src and not img.src:match("^https?://") then
    ensure_root()
    local src = url_decode(img.src)
    img.src = src
    local abs = pandoc.path.join({ root, src })
    if not file_exists(abs) then
      if src:find("paper_artifacts/") then
        local alt = src:gsub("paper_artifacts/", "assets/")
        local abs2 = pandoc.path.join({ root, alt })
        if file_exists(abs2) then
          img.src = alt
        end
      elseif src:find("assets/") then
        local alt = src:gsub("assets/", "paper_artifacts/")
        local abs2 = pandoc.path.join({ root, alt })
        if file_exists(abs2) then
          img.src = alt
        end
      end
    end
  end
  return img
end

function Figure(el)
  local captext = pandoc.utils.stringify(el.caption)
  if captext and captext ~= "" then
    fig = fig + 1
    el.caption = pandoc.Caption(pandoc.Plain(make_caption_inlines(captext)))
  end
  return el
end

function Pandoc(doc)
  local new_blocks = {}
  local i = 1
  while i <= #doc.blocks do
    local b = doc.blocks[i]
    if b.t == "Header" and b.level == 2 then
      -- 尝试从标题文本中提取章节号
      local text = pandoc.utils.stringify(b)
      local num = text:match("第%s*(%d+)%s*章")
      if num then
        chapter = tonumber(num)
      else
        chapter = chapter + 1
      end
      
      fig = 0
      table.insert(new_blocks, b)
    elseif b.t == "Para" or b.t == "Plain" then
      if #b.content == 1 and b.content[1].t == "Image" then
        local img = b.content[1]
        local cap = img.caption and pandoc.utils.stringify(img.caption) or nil
        if cap and #cap > 0 then
          fig = fig + 1
          img.caption = make_caption_inlines(cap)
          table.insert(new_blocks, b)
        else
          local nextb = doc.blocks[i + 1]
          if nextb and (nextb.t == "Para" or nextb.t == "Plain" or nextb.t == "BlockQuote") then
            local text = nil
            if nextb.t == "BlockQuote" then
              if #nextb.content >= 1 and (nextb.content[1].t == "Para" or nextb.content[1].t == "Plain") then
                text = pandoc.utils.stringify(nextb.content[1])
              end
            else
              text = pandoc.utils.stringify(nextb)
            end
            if text and #text > 0 then
              fig = fig + 1
              img.caption = make_caption_inlines(text)
              table.insert(new_blocks, b)
              i = i + 1
            else
              table.insert(new_blocks, b)
            end
          else
            table.insert(new_blocks, b)
          end
        end
      else
        table.insert(new_blocks, b)
      end
    elseif b.t == "BlockQuote" then
      local content = b.content
      if #content >= 1 and (content[1].t == "Para" or content[1].t == "Plain") then
        local first = content[1]
        if #first.content == 1 and first.content[1].t == "Image" then
          local img = first.content[1]
          local cap = img.caption and pandoc.utils.stringify(img.caption) or nil
          local text = cap
          if (not text or #text == 0) and #content >= 2 and (content[2].t == "Para" or content[2].t == "Plain") then
            text = pandoc.utils.stringify(content[2])
          end
          if text and #text > 0 then
            fig = fig + 1
            img.caption = make_caption_inlines(text)
            table.insert(new_blocks, b)
          else
            table.insert(new_blocks, b)
          end
        else
          table.insert(new_blocks, b)
        end
      else
        table.insert(new_blocks, b)
      end
    else
      table.insert(new_blocks, b)
    end
    i = i + 1
  end
  return pandoc.Pandoc(new_blocks, doc.meta)
end
